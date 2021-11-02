package io.deephaven.integrations.learn.PopulateTensorExample

import io.deephaven.db.v2.sources.ColumnSource;

/**
 * Example of copying data from a table into a tensor.
 *
 * 1. One of these two should be much faster than the other.
 * 2. There need to be many of these functions with different tensor types to handle different numpy inputs.
 * 3. There may need to be some sort of special logic to retrieve values from columns of different types and get the values in a type that can be used to fill the tensor.  See `Java2NumpyCopy` for ideas.
 */
public class PopulateTensorExample {


    /**
     * Copy data from a table into a 2d tensor.
     *
     * @param indexSet indices of the rows of the table to put into the tensor
     * @param columnSources columns of data to put into the tensor
     * @param tensor contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here. 
     */
    public static void populate_tensor_2d_v1(final IndexSet indexSet, final ColumnSource[] columnSources, final final double[] tensor) {
        final int nRows = indexSet.getSize();
        final int nCols = columnSources.length;

        if( tensor.length != nRows * nCols ){
            throw new RuntimeException("Tensor size does not match ....");
        }

        int i = 0;
        for( long idx : indexSet ) {
            int j = 0;

            for( ColumnSource cs : columnSources ) {
                final int ij = nCols * i + j;
                rst[ij] = cs.get(idx);
                j++;
            }

            i++;
        }
    }

    /**
     * Copy data from a table into a 2d tensor.
     *
     * @param indexSet indices of the rows of the table to put into the tensor
     * @param columnSources columns of data to put into the tensor
     * @param tensor contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here. 
     */
    public static void populate_tensor_2d_v2(final IndexSet indexSet, final ColumnSource[] columnSources, final final double[] tensor) {
        final int nRows = indexSet.getSize();
        final int nCols = columnSources.length;

        if( tensor.length != nRows * nCols ){
            throw new RuntimeException("Tensor size does not match ....");
        }

        int j = 0;
        for( ColumnSource cs : columnSources ) {
            int i = 0;

            for( long idx : indexSet ) {
                final int ij = nCols * i + j;
                rst[ij] = cs.get(idx);
                i++;
            }

            j++;
        }
    }

}