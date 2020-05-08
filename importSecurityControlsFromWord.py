from docx import Document
import dbFunctions as dbFct


def getCheckedOptions(cell):
    results = []
    cell_elm = cell._element
    # checkBoxes = cell_elm.xpath('.//w14:checkBox')
    checkBoxes = cell_elm.xpath(".//*[local-name()='checked']")
    labels = cell_elm.xpath(".//*[local-name()='t']")
    c = 0
    for item in labels:
        if type(item.text) == str:
            if item.text != "Implementation Status (check all that apply):" and item.text != "Control Origination (check all that apply):" and c < len(checkBoxes):
                if checkBoxes[c].values()[0] == '1':
                    results.append(item.text)
                c = c + 1
    return ','.join(results)

def main(document,db,system_id):
    controlSummary = {}
    controlResponse = {}
    parameterList = []
    d = Document(document)
    for table in d.tables:
        firstRow = True
        # There are 2 kinds of tables, Control Summary and solution
        # Sometimes the solution table has only 1 column and sometimes it has 2
        columns = len(table.rows[0].cells)
        if table.rows[0].cells[0].text != table.rows[0].cells[columns-1].text:
            if table.rows[0].cells[1].text == "Control Summary Information":
                control_id = table.rows[0].cells[0].text
                controlSummary["control_id"] = control_id
                controlSummary["responsableRole"] = table.rows[1].cells[0].text
                # there can be a variable number of paramaters so we ahve to go dynamic now
                for row in table.rows:
                    content = row.cells[0].text
                    if content[0:9] == "Parameter":
                        parameterList.append(content)
                    if content[0:14] == "Implementation":
                        # controlSummary["implementationStatus"] = content
                        controlSummary["implementationStatus"] = getCheckedOptions(row.cells[0])
                    if content[0:7] == "Control":
                        controlSummary["controlOrigination"] = getCheckedOptions(row.cells[0])
                controlSummary["parameterList"] = ', '.join(parameterList)
                controlSummary["system_id"] = str(system_id)
                sql = dbFct.insertFromDict("securityControls", controlSummary)
                dbFct.UpdateDB(sql, controlSummary, db)
            else:
                msg = '|'
                for item in table.rows[0].cells:
                    msg = msg + item.text + '|'
                #print "Table not imported. First Row text was "
                #print msg
        else:
            rowCount = 0
            for row in table.rows:
                #skip header row
                if firstRow:
                    firstRow = False
                    t = row.cells[0].text
                    control_id = t[0:t.find(' What')]
                else:
                    controlResponse["control_id"] = control_id
                    # Handle the case where the table has only 1 column
                    if len(row.cells) == 1:
                        controlResponse["part"] = "Part a"
                        controlResponse["value"] = row.cells[0].text
                    else:
                        controlResponse["part"] = row.cells[0].text
                        controlResponse["value"] = row.cells[1].text
                    controlResponse["system_id"] = str(system_id)
                    sql = dbFct.insertFromDict("controlResponse", controlResponse)
                    dbFct.UpdateDB(sql, controlResponse, db)
                    rowCount = rowCount+1
        # reset the containers
        controlResponse = {}
        controlSummary = {}
        parameterList = []
