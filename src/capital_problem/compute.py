import pandas
import numpy
import similaritymeasures


def stats_between_series(
    xaxis_1: pandas.Series,
    values_1: pandas.Series,
    xaxis_2: pandas.Series,
    values_2: pandas.Series,
    print_: bool = False,
) -> dict:
    """Dynamic time warping and discret frechet distance for measuring similarity between two temporal sequences

    Args:
        xaxis_1 (pandas.Series): index axis of the dataframe 1
        values_1 (pandas.Series): value axis of the dataframe 1
        xaxis_2 (pandas.Series): index axis of the dataframe 2
        values_2 (pandas.Series): value axis of the dataframe 2

    Returns:
        dict: `{"dtw": float, "frechet_dist": float}`
    """

    dataframe_1 = pandas.merge(xaxis_1, values_1, right_index=True, left_index=True)
    dataframe_2 = pandas.merge(xaxis_2, values_2, right_index=True, left_index=True)

    dataframe_1.rename(
        columns={xaxis_1.name: "id", values_1.name: "values_1"}, inplace=True
    )
    dataframe_2.rename(
        columns={xaxis_2.name: "id", values_2.name: "values_2"}, inplace=True
    )

    dataframe_1.set_index("id", inplace=True)
    dataframe_2.set_index("id", inplace=True)

    unified = pandas.concat([dataframe_1, dataframe_2], axis=1)
    unified["values_1"] = (
        pandas.to_numeric(unified["values_1"], errors="coerce", downcast="float")
        .interpolate()
        .fillna(method="bfill")
        .fillna(method="ffill")
    )
    unified["values_2"] = (
        pandas.to_numeric(unified["values_2"], errors="coerce", downcast="float")
        .interpolate()
        .fillna(method="bfill")
        .fillna(method="ffill")
    )

    xaxis_arranged = numpy.arange(len(unified))
    dataframe_values_2 = numpy.array([xaxis_arranged, unified["values_2"].values])
    dataframe_values_1 = numpy.array([xaxis_arranged, unified["values_1"].values])

    dtw, d = similaritymeasures.dtw(dataframe_values_1, dataframe_values_2)

    frechet_dist = similaritymeasures.frechet_dist(
        dataframe_values_1, dataframe_values_2
    )

    pcm = similaritymeasures.pcm(dataframe_values_1, dataframe_values_2)

    area = similaritymeasures.area_between_two_curves(
        dataframe_values_1, dataframe_values_2
    )

    std = numpy.abs(
        numpy.nanstd(dataframe_values_2[1]) - numpy.nanstd(dataframe_values_1[1])
    )

    if print_:
        print(
            {
                "dtw": dtw,
                "frechet_dist": frechet_dist,
                "pcm": pcm,
                "area": area,
                "std": std,
            },
            dataframe_values_2,
        )

    return {
        "dtw": dtw,
        "frechet_dist": frechet_dist,
        "pcm": pcm,
        "area": area,
        "std": std,
    }
