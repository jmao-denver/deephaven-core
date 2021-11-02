package io.deephaven.integrations.learn;

import io.deephaven.db.tables.Table;
import io.deephaven.db.v2.sources.ColumnSource;

import java.util.Arrays;


//import numpy as np
//from deephaven.TableTools import emptyTable
//
//PopulateTensorExample = jpy.get_type("io.deephaven.integrations.learn.PopulateTensorExample")
//
//## This commented out stuff is only needed if there are memory leaks.
//
//# def gather1(index_set, col_sources, dtype=np.float64):
//#     nRow = index_set.getSize()
//#     nCol = len(col_sources)
//#     tensor = np.empty([nRow, nCol], dtype=dtype, order="C")
//#     print("DBG: tensor_start\n", tensor)
//#     PopulateTensorExample.populate_tensor_2d_v1(index_set, col_sources, tensor)
//#     print("DBG: tensor_end\n", tensor)
//#     return tensor
//
//# def gather2(index_set, col_sources, dtype=np.float64):
//#     nRow = index_set.getSize()
//#     nCol = len(col_sources)
//#     tensor = np.empty([nRow, nCol], dtype=dtype, order="C")
//#     print("DBG: tensor_start\n", tensor)
//#     PopulateTensorExample.populate_tensor_2d_v2(index_set, col_sources, tensor)
//#     print("DBG: tensor_end\n", tensor)
//#     return tensor
//
//###
//
//def ggather1(index_set, col_sources, dtype=np.float64):
//    nRow = index_set.getSize()
//    nCol = len(col_sources)
//    buffer = PopulateTensorExample.create_tensor_2d_v1(index_set, col_sources)
//    # print("DBG: buffer ", buffer)
//    tensor = np.frombuffer(buffer, dtype=dtype)
//    tensor.shape = (nRow, nCol)
//    # print("DBG: tensor\n", tensor)
//    return tensor
//
//def ggather2(index_set, col_sources, dtype=np.float64):
//    nRow = index_set.getSize()
//    nCol = len(col_sources)
//    buffer = PopulateTensorExample.create_tensor_2d_v2(index_set, col_sources)
//    # print("DBG: buffer ", buffer)
//    tensor = np.frombuffer(buffer, dtype=dtype)
//    tensor.shape = (nRow, nCol)
//    # print("DBG: tensor\n", tensor)
//    return tensor
//
//###
//
//
//t = emptyTable(3).update("X = (double)i", "Y = 2*X")
//col_sources = [ t.getColumnSource(col) for col in ["X", "Y"] ]
//index_set = PopulateTensorExample.makeIndexSet(t);
//
//# tensor_1 = gather1(index_set, col_sources)
//# print(tensor_1)
//# tensor_2 = gather2(index_set, col_sources)
//# print(tensor_2)
//
//
//gtensor_1 = ggather1(index_set, col_sources)
//print(gtensor_1)
//gtensor_2 = ggather2(index_set, col_sources)
//print(gtensor_2)
//
//
//#####
//
//def check_memory_leaks(n_rows = 10000, n_mem_checks = 100_000_000, n_print = 1_000_000)
//    print("***** CHECK FOR MEMORY LEAKS *****")
//    t = emptyTable(n_rows).update("X = (double)i", "Y = 2*X")
//    col_sources = [ t.getColumnSource(col) for col in ["X", "Y"] ]
//    index_set = PopulateTensorExample.makeIndexSet(t);
//
//    for i in range(1,n_mem_checks+1):
//        if i%n_print == 0:
//            print(f"Memory leak check: {i}")
//        tensor_1 = ggather1(index_set, col_sources)
//        tensor_2 = ggather2(index_set, col_sources)
//


/**
 * Example of copying data from a table into a tensor.
 *
 * 1. One of these two should be much faster than the other.
 * 2. There need to be many of these functions with different tensor types to handle different numpy inputs.
 * 3. There may to be some sort of special logic to retrieve values from columns of different types and get the values
 *    in a type that can be used to fill the tensor without duplicating a bunch of code.
 *    See `Java2NumpyCopy` for ideas on how to structure this.
 */
public class PopulateTensorExample {

    /**
     * Generate an index set from a table.
     * THIS IS JUST TO CREATE THE ILLUSTRATION BY HACKING STUFF IN PYTHON.  NOT NEEDED FOR PROD.
     *
     * @param t table
     * @return index set
     */
    public static IndexSet makeIndexSet(final Table t) {
        final IndexSet is = new IndexSet(t.intSize());

        for(long idx : t.getIndex()) {
            is.add(idx);
        }

        return is;
    }

//    /**
//     * Copy data from a table into a 2d tensor.
//     *
//     * @param indexSet indices of the rows of the table to put into the tensor
//     * @param columnSources columns of data to put into the tensor
//     * @param tensor contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here.
//     */
//    public static void populate_tensor_2d_v1(final IndexSet indexSet, final ColumnSource<?>[] columnSources, final double[] tensor) {
//        final int nRows = indexSet.getSize();
//        final int nCols = columnSources.length;
//
//        if( tensor.length != nRows * nCols ) {
//            throw new RuntimeException("Tensor size does not match ....");
//        }
//
//        int i = 0;
//        for( long idx : indexSet ) {
//            int j = 0;
//
//            for( ColumnSource<?> cs : columnSources ) {
//                final int ij = nCols * i + j;
//                System.out.println("V1 (" + i + "," + j + "; " + ij + ") [" + idx + "] = " + cs.getDouble(idx));
//                tensor[ij] = cs.getDouble(idx);
//                j++;
//            }
//
//            i++;
//        }
//
//        System.out.println("V1 = " + Arrays.toString(tensor));
//    }
//
//    /**
//     * Copy data from a table into a 2d tensor.
//     *
//     * @param indexSet indices of the rows of the table to put into the tensor
//     * @param columnSources columns of data to put into the tensor
//     * @param tensor contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here.
//     */
//    public static void populate_tensor_2d_v2(final IndexSet indexSet, final ColumnSource<?>[] columnSources, final double[] tensor) {
//        final int nRows = indexSet.getSize();
//        final int nCols = columnSources.length;
//
//        if( tensor.length != nRows * nCols ) {
//            throw new RuntimeException("Tensor size does not match ....");
//        }
//
//        int j = 0;
//        for( ColumnSource<?> cs : columnSources ) {
//            int i = 0;
//
//            for( long idx : indexSet ) {
//                final int ij = nCols * i + j;
//                System.out.println("V2 (" + i + "," + j + "; " + ij + ") [" + idx + "] = " + cs.getDouble(idx));
//                tensor[ij] = cs.getDouble(idx);
//                i++;
//            }
//
//            j++;
//        }
//
//        System.out.println("V2 = " + Arrays.toString(tensor));
//    }

    /**
     * Copy data from a table into a 2d tensor.
     *
     * @param indexSet indices of the rows of the table to put into the tensor
     * @param columnSources columns of data to put into the tensor
     * @return  contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here.
     */
    public static double[] create_tensor_2d_v1(final IndexSet indexSet, final ColumnSource<?>[] columnSources) {
        final int nRows = indexSet.getSize();
        final int nCols = columnSources.length;
        final double[] tensor = new double[nRows * nCols];

        int i = 0;
        for( long idx : indexSet ) {
            int j = 0;

            for( ColumnSource<?> cs : columnSources ) {
                final int ij = nCols * i + j;
//                System.out.println("V1 (" + i + "," + j + "; " + ij + ") [" + idx + "] = " + cs.getDouble(idx));
                tensor[ij] = cs.getDouble(idx);
                j++;
            }

            i++;
        }

//        System.out.println("V1 = " + Arrays.toString(tensor));
        return tensor;
    }

    /**
     * Copy data from a table into a 2d tensor.
     *
     * @param indexSet indices of the rows of the table to put into the tensor
     * @param columnSources columns of data to put into the tensor
     * @return contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here.
     */
    public static double[] create_tensor_2d_v2(final IndexSet indexSet, final ColumnSource<?>[] columnSources) {
        final int nRows = indexSet.getSize();
        final int nCols = columnSources.length;
        final double[] tensor = new double[nRows * nCols];

        int j = 0;
        for( ColumnSource<?> cs : columnSources ) {
            int i = 0;

            for( long idx : indexSet ) {
                final int ij = nCols * i + j;
//                System.out.println("V2 (" + i + "," + j + "; " + ij + ") [" + idx + "] = " + cs.getDouble(idx));
                tensor[ij] = cs.getDouble(idx);
                i++;
            }

            j++;
        }

//        System.out.println("V2 = " + Arrays.toString(tensor));
        return tensor;
    }

}