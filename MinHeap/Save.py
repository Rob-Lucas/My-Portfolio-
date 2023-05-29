    i = parent
    while i < da.length()-1:
        left_child_index = (2 * i) + 1
        right_child_index = (2 * i) + 2

        # if left child exists and is less than parent
        if left_child_index < da.length() and da[left_child_index] < da[i]:
            # if right child exists and is less than left child
            if right_child_index < da.length() and da[right_child_index] < da[left_child_index]:
                da[i], da[right_child_index] = da[right_child_index], da[i]
                i = right_child_index
            else:
                da[i], da[left_child_index] = da[left_child_index], da[i]
                i = left_child_index
        # if right child exists and is less than parent
        elif right_child_index < da.length() and da[right_child_index] < da[i]:
            da[i], da[right_child_index] = da[right_child_index], da[i]
            i = right_child_index
        else:
            break



    for i in range(da.length()//2-1, da.length()-1, -1):
        _percolate_down(da, i)

    # Sort the array by repeatedly removing the min element and restoring the heap property
    for i in range(da.length() -1, 0, -1):
        da[0], da[i] = da[i], da[0]
        _percolate_down(da, 0)

    left_cursor = 0
    right_cursor = da.length()-1
    # reverses the sort of the list
    while left_cursor != right_cursor:
        save = da[right_cursor]
        da[right_cursor] = da[left_cursor]
        da[left_cursor] = save
        left_cursor += 1
        right_cursor -= 1



    n = da.length()
    for i in range(n // 2 - 1, -1, -1):
        j = i
        while 2 * j + 1 < n:
            k = 2 * j + 1
            if k + 1 < n and da[k + 1] > da[k]:
                k += 1
            if da[k] > da[j]:
                da[k],da[j] = da[j],da[k]
                j = k
            else:
                break
    
    # Next, perform the heap sort by repeatedly removing the maximum element
    # and placing it at the end of the array
    for i in range(n-1, 0, -1):
        da[0],da[i] = da[i],da[0]
        j = 0
        while 2 * j + 1 < i:
            k = 2 * j + 1
            if k + 1 < i and da[k + 1] > da[k]:
                k += 1
            if da[k] > da[j]:
                da[k],da[j] = da[j],da[k]
                j = k
            else:
                break