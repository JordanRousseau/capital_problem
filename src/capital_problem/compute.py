import pandas
import numpy


def area_between(
    xaxis_1: pandas.Series,
    values_1: pandas.Series,
    xaxis_2: pandas.Series,
    values_2: pandas.Series,
) -> float:
    """Compute area between two ordered dataframes

    Args:
        xaxis_1 (pandas.Series): index axis of the dataframe 1
        values_1 (pandas.Series): value axis of the dataframe 1
        xaxis_2 (pandas.Series): index axis of the dataframe 2
        values_2 (pandas.Series): value axis of the dataframe 2

    Returns:
        float: Area between curves
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

    print(dataframe_2, dataframe_1)

    unified = pandas.concat([dataframe_1, dataframe_2], axis=1)
    unified["values_1"] = pandas.to_numeric(
        unified["values_1"], errors="coerce", downcast="float"
    ).interpolate()
    unified["values_2"] = pandas.to_numeric(
        unified["values_2"], errors="coerce", downcast="float"
    ).interpolate()

    # let us generate fake test data
    xaxis_arranged = numpy.arange(len(unified))
    dataframe_values_1[:, 1] = xaxis_arranged
    dataframe_values_2[:, 1] = xaxis_arranged
    dataframe_values_1[:, 1] = unified["values_1"].values
    dataframe_values_2[:, 1] = unified["values_2"].values
    y2 = unified["values_2"].values

    return similaritymeasures.area_between_two_curves(
        dataframe_values_1, dataframe_values_2
    )


if __name__ == "__main__":
    area_between(
        xaxis_1=pandas.Series(["a", "b", "c", "e"], name="id"),
        values_1=pandas.Series(["1", "2", "4", "1"], name="values"),
        xaxis_2=pandas.Series(["a", "b", "d", "e"], name="id2"),
        values_2=pandas.Series(["1", "7", "7", "1"], name="values2"),
    )
