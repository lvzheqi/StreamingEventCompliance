def build_deviation_pdf(client_uuid):
    '''
    Creates a deviation PDF for the given client_uuid, based on the deviations history
    stored in AlertLog entity in database. This pdf is stored in local as “<client_uuid>_deviations.pdf”.
    :param client_uuid: user name
    :return: whether the file is created successfully
    '''
    return True


def show_deviation_pdf(client_uuid):
    '''
    Returns the file “<client_uuid>_deviations.pdf”  if present in the local.
    Else if no file present with that name then, this function calls the build_deviation_pdf(client_uuid) to create a pdf
    :param client_uuid: user name
    :return: PDF File
    '''
    # TODO: show the pdf to different client
    return "pdf"

