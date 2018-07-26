import numpy as np

def km_max(profit_matrix):
    """ Solve the linear sum assignment problem.
    the linear sum assignment problem is known as maximum weight matching
    in bipartite graghs. A problem 

    Formaly, let x be a boolen matrix where: math:='X[i,j]=1' iff row i is
    assigned to column j. Then the optimal assignment has Profit 
    .. math ::
        \max\sum_i\sum_j profit_{i,j} x_{i,j}
    s.t each row is assignment to as most one column, and each column to 
    at most one row.

    The method used is the Hungarian algorithm, also known as the Mukres 
    or kuhn-Munhres algorithm.
    
    This script refers to linear_sum assignment method from scipy.optimize.
    I did a bit revision.

    @Parameters
    -------------
    # Hungarian algorithm (Kuhn-Munkres) for solving the linear sum assignment
    ----------
    profit_matrix : array
        The profit matrix of the bipartite graph.

    Returns
    -------
    row_ind, col_ind : array
        An array of row indices and one of corresponding column indices giving
        the optimal assignment. The profit of the assignment can be computed
        as ``profit_matrix[row_ind, col_ind].sum()``. The row indices will be
        sorted; in the case of a square profit matrix they will be equal to
        ``numpy.arange(profit_matrix.shape[0])``.

    Notes
    -----
    .. versionadded:: 0.17.0

    Examples
    --------
    >>> profit = np.array([[4, 1, 3], [2, 0, 5], [3, 2, 2]])
    >>> import km
    >>> row_ind, col_ind = km.km_max(profit)
    >>> col_ind
    array([1, 0, 2])
    >>> profit[row_ind, col_ind].sum()
    

    References
    ----------
    1. http://csclab.murraystate.edu/bob.pilgrim/445/munkres.html

    2. Harold W. Kuhn. The Hungarian Method for the assignment problem.
       *Naval Research Logistics Quarterly*, 2:83-97, 1955.

    3. Harold W. Kuhn. Variants of the Hungarian method for assignment
       problems. *Naval Research Logistics Quarterly*, 3: 253-258, 1956.

    4. Munkres, J. Algorithms for the Assignment and Transportation Problems.
       *J. SIAM*, 5(1):32-38, March, 1957.

    5. https://en.wikipedia.org/wiki/Hungarian_algorithm
    """
    profit_matrix = np.asarray(profit_matrix)
    if len(profit_matrix.shape) != 2:
        raise ValueError("expected a matrix (2-d array), got a %r array"
                         % (profit_matrix.shape,))

    # The algorithm expects more columns than rows in the profit matrix.
    if profit_matrix.shape[1] < profit_matrix.shape[0]:
        profit_matrix = profit_matrix.T
        transposed = True
    else:
        transposed = False

    state = _Hungary(profit_matrix)

    # No need to bother with assignments if one of the dimensions
    # of the profit matrix is zero-length.
    step = None if 0 in profit_matrix.shape else _step1

    while step is not None:
        step = step(state)

    if transposed:
        marked = state.marked.T
    else:
        marked = state.marked
    return np.where(marked == 1)


class _Hungary(object):
    """State of the Hungarian algorithm.

    Parameters
    ----------
    profit_matrix : 2D matrix
        The profit matrix. Must have shape[1] >= shape[0].
    """

    def __init__(self, profit_matrix):
        self.C = profit_matrix.copy()

        n, m = self.C.shape
        self.row_uncovered = np.ones(n, dtype=bool)
        self.col_uncovered = np.ones(m, dtype=bool)
        self.Z0_r = 0
        self.Z0_c = 0
        self.path = np.zeros((n + m, 2), dtype=int)
        self.marked = np.zeros((n, m), dtype=int)

    def _clear_covers(self):
        """Clear all covered matrix cells"""
        self.row_uncovered[:] = True
        self.col_uncovered[:] = True


# Individual steps of the algorithm follow, as a state machine: they return
# the next step to be taken (function to be called), if any.

def _step1(state):
    """Steps 1 and 2 in the Wikipedia page."""

    # Step 1: For each row of the matrix, find the biggest element and
    # subtract it from every element in its row.
    state.C -= state.C.max(axis=1)[:, np.newaxis]
    # Step 2: Find a zero (Z) in the resulting matrix. If there is no
    # starred zero in its row or column, star Z. Repeat for each element
    # in the matrix.
    for i, j in zip(*np.where(state.C == 0)):
        if state.col_uncovered[j] and state.row_uncovered[i]:
            state.marked[i, j] = 1
            state.col_uncovered[j] = False
            state.row_uncovered[i] = False

    state._clear_covers()
    return _step3


def _step3(state):
    """
    Cover each column containing a starred zero. If n columns are covered,
    the starred zeros describe a complete set of unique assignments.
    In this case, Go to DONE, otherwise, Go to Step 4.
    """
    marked = (state.marked == 1)
    state.col_uncovered[np.any(marked, axis=0)] = False

    if marked.sum() < state.C.shape[0]:
        return _step4


def _step4(state):
    """
    Find a noncovered zero and prime it. If there is no starred zero
    in the row containing this primed zero, Go to Step 5. Otherwise,
    cover this row and uncover the column containing the starred
    zero. Continue in this manner until there are no uncovered zeros
    left. Save the biggest uncovered value and Go to Step 6.
    """
    # We convert to int as numpy operations are faster on int
    C = (state.C == 0).astype(int)
    covered_C = C * state.row_uncovered[:, np.newaxis]
    covered_C *= np.asarray(state.col_uncovered, dtype=int)
    n = state.C.shape[0]
    m = state.C.shape[1]

    while True:
        # Find an uncovered zero
        row, col = np.unravel_index(np.argmax(covered_C), (n, m))
        if covered_C[row, col] == 0:
            return _step6
        else:
            state.marked[row, col] = 2
            # Find the first starred element in the row
            star_col = np.argmax(state.marked[row] == 1)
            if state.marked[row, star_col] != 1:
                # Could not find one
                state.Z0_r = row
                state.Z0_c = col
                return _step5
            else:
                col = star_col
                state.row_uncovered[row] = False
                state.col_uncovered[col] = True
                covered_C[:, col] = C[:, col] * (
                    np.asarray(state.row_uncovered, dtype=int))
                covered_C[row] = 0


def _step5(state):
    """
    Construct a series of alternating primed and starred zeros as follows.
    Let Z0 represent the uncovered primed zero found in Step 4.
    Let Z1 denote the starred zero in the column of Z0 (if any).
    Let Z2 denote the primed zero in the row of Z1 (there will always be one).
    Continue until the series terminates at a primed zero that has no starred
    zero in its column. Unstar each starred zero of the series, star each
    primed zero of the series, erase all primes and uncover every line in the
    matrix. Return to Step 3
    """
    count = 0
    path = state.path
    path[count, 0] = state.Z0_r
    path[count, 1] = state.Z0_c

    while True:
        # Find the first starred element in the col defined by
        # the path.
        row = np.argmax(state.marked[:, path[count, 1]] == 1)
        if state.marked[row, path[count, 1]] != 1:
            # Could not find one
            break
        else:
            count += 1
            path[count, 0] = row
            path[count, 1] = path[count - 1, 1]

        # Find the first prime element in the row defined by the
        # first path step
        col = np.argmax(state.marked[path[count, 0]] == 2)
        if state.marked[row, col] != 2:
            col = -1
        count += 1
        path[count, 0] = path[count - 1, 0]
        path[count, 1] = col

    # Convert paths
    for i in range(count + 1):
        if state.marked[path[i, 0], path[i, 1]] == 1:
            state.marked[path[i, 0], path[i, 1]] = 0
        else:
            state.marked[path[i, 0], path[i, 1]] = 1

    state._clear_covers()
    # Erase all prime markings
    state.marked[state.marked == 2] = 0
    return _step3


def _step6(state):
    """
    Add the value found in Step 4 to every element of each covered row,
    and subtract it from every element of each uncovered column.
    Return to Step 4 without altering any stars, primes, or covered lines.
    """
    # the biggest uncovered value in the matrix
    if np.any(state.row_uncovered) and np.any(state.col_uncovered):
        maxval = np.max(state.C[state.row_uncovered], axis=0)
        maxval = np.max(maxval[state.col_uncovered])
        state.C[~state.row_uncovered] += maxval
        state.C[:, state.col_uncovered] -= maxval
    return _step4

