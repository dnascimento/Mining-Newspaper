def swap(vector,a,b):
    value = vector[a]
    vector[a] = vector[b]
    vector[b] = value


def quicksort(A,low,high):
    if low < high: 
        pivot_location = partition(A,low,high)
        quicksort(A,low,pivot_location-1)
        quicksort(A,pivot_location+1,high)

def partition(A,low,high):
    #pivot e o 1o elemento do subarray
    pivot = A[low]      
    #o leftwall e o numero index menor que atras dele esta ordenado
    leftwall = low     
        
    for i,w in enumerate(A[low+1:high]):
        i = low+1+i
        if w < pivot:
            leftwall = leftwall + 1;
            swap(A,i,leftwall)
    swap(A,low,leftwall)
    return leftwall
    


