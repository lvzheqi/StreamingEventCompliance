import pandas as pd

from pm4py.objects.log import log as log_instance
from pm4py.objects.log import transform as log_transform


def get_dataframe_from_log(log):
    """
    Return a Pandas dataframe from a given logger

    Parameters
    -----------
    log: :class:`pm4py.logger.logger.EventLog`
        Event logger. Also, can take a trace logger and convert it to event logger

    Returns
    -----------
    df
        Pandas dataframe
    """
    if type(log) is log_instance.TraceLog:
        log = log_transform.transform_trace_log_to_event_log(log)
    transf_log = [dict(x) for x in log]
    df = pd.DataFrame.from_dict(transf_log)

    return df


def export_log_as_string(log, parameters=None):
    """
    Exports the given logger to string format

    Parameters
    -----------
    log: :class:`pm4py.logger.logger.EventLog`
        Event logger. Also, can take a trace logger and convert it to event logger
    parameters
        Possible parameters of the algorithm

    Returns
    -----------
    string
        String representing the CSV logger
    """
    if parameters is None:
        parameters = {}
    del parameters

    df = get_dataframe_from_log(log)

    return df.to_string()


def export_log(log, output_file_path, parameters=None):
    """
    Exports the given logger to CSV format

    Parameters
    ----------
    log: :class:`pm4py.logger.logger.EventLog`
        Event logger. Also, can take a trace logger and convert it to event logger
    output_file_path:
        Output file path
    parameters
        Possible parameters of the algorithm
    """
    if parameters is None:
        parameters = {}
    del parameters

    df = get_dataframe_from_log(log)
    df.to_csv(output_file_path)
