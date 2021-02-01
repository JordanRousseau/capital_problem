import pandas
import numpy
import similaritymeasures


def stats_between_series(
    xaxis_1: pandas.Series,
    values_1: pandas.Series,
    xaxis_2: pandas.Series,
    values_2: pandas.Series,
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

    dataframe_1 = pandas.concat([xaxis_1, values_1, xaxis_2, values_2], axis=1)
    return dataframe_1


if __name__ == "__main__":
    print(
        stats_between_series(
            xaxis_1=pandas.Series(["a", "b", "c", "e"], name="id"),
            values_1=pandas.Series(["1", "2", "4", "1"], name="values"),
            xaxis_2=pandas.Series(["a", "b", "d", "e"], name="id2"),
            values_2=pandas.Series(["1", "7", "7", "1"], name="values2"),
        )
    )