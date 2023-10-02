# bucket sorting mechanism

data = [5, 3, 1, 2, 4, 6, 7, 8, 9, 10]


def bucket_sorting(arr):
    # get the maximum value from the array
    max_value = max(arr)
    # create a bucket with the size of max_value + 1
    bucket = [0] * (max_value + 1)
    # loop through the array
    for i in arr:
        # increment the value of the bucket at the index of the current value of the array
        bucket[i] += 1
    # create a new array
    new_arr = []
    # loop through the bucket
    for i in range(len(bucket)):
        # loop through the value of the bucket at the current index
        for j in range(bucket[i]):
            # append the index to the new array
            new_arr.append(i)
    # return the new array
    return new_arr


print(bucket_sorting(data))


