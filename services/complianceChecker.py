from services import deviationPDF


def compliance_checker(client_uuid, event):
    print('case_id: ', event['case_id'])
    print('activity: ', event['activity'])
    # TODO: analyse and write non-compliance event to the database AlertLog with client_uuid

    if event['case_id'] == 'NONE' and event['activity'] == 'END':
        deviationPDF.build_deviation_pdf(client_uuid)

    return 'deviation'


def error_handle():
    return "error"

