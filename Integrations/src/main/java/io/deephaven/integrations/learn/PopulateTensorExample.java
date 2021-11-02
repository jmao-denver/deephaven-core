package io.deephaven.integrations.learn;

import io.deephaven.db.tables.Table;
import io.deephaven.db.v2.sources.ColumnSource;

import java.util.Arrays;


/*

import numpy as np
from deephaven.TableTools import emptyTable
from time import time

PopulateTensorExample = jpy.get_type("io.deephaven.integrations.learn.PopulateTensorExample")

def gather1(index_set, col_sources, dtype=np.float64):
    nRow = index_set.getSize()
    nCol = len(col_sources)
    buffer = PopulateTensorExample.create_tensor_2d_v1(index_set, col_sources)
    # print("DBG: buffer ", buffer)
    tensor = np.frombuffer(buffer, dtype=dtype)
    tensor.shape = (nRow, nCol)
    # print("DBG: tensor\n", tensor)
    return tensor

def gather2(index_set, col_sources, dtype=np.float64):
    nRow = index_set.getSize()
    nCol = len(col_sources)
    buffer = PopulateTensorExample.create_tensor_2d_v2(index_set, col_sources)
    # print("DBG: buffer ", buffer)
    tensor = np.frombuffer(buffer, dtype=dtype)
    tensor.shape = (nRow, nCol)
    # print("DBG: tensor\n", tensor)
    return tensor

def gather_legacy(idx, cols):
    rst = np.empty([idx.getSize(), len(cols)], dtype = np.float)
    iter = idx.iterator()
    i = 0
    while (iter.hasNext()):
        it = iter.next()
        j = 0
        for col in cols:
            rst[i, j] = col.get(it)
            j += 1
        i += 1

    return np.squeeze(rst)

###

def make_test_inputs(n_rows):
    t = emptyTable(n_rows).update("X = (double)i", "Y = 2*X")
    col_sources = [ t.getColumnSource(col) for col in ["X", "Y"] ]
    index_set = PopulateTensorExample.makeIndexSet(t)
    return t, col_sources, index_set

#####

t, col_sources, index_set = make_test_inputs(3)

tensor_1 = gather1(index_set, col_sources)
print(tensor_1)
tensor_2 = gather2(index_set, col_sources)
print(tensor_2)
tensor_legacy = gather_legacy(index_set, col_sources)
print(tensor_legacy)

#####

def perf_check(n_repeat=10, n_rows_set=[1_000, 10_000, 100_000, 1_000_000, 10_000_000]):
    print("SPEEDUP:\tV1\tV2\tLEGACY")

    for n_rows in n_rows_set:
        t, col_sources, index_set = make_test_inputs(n_rows)

        tm0 = time()
        for i in range(n_repeat):
            tensor_1 = gather1(index_set, col_sources)
        tm1 = time()
        for i in range(n_repeat):
            tensor_2 = gather2(index_set, col_sources)
        tm2 = time()
        for i in range(n_repeat):
            tensor_legacy = gather_legacy(index_set, col_sources)
        tm3 = time()
        tm_v1 = tm1-tm0
        tm_v2 = tm2-tm1
        tm_legacy = tm3-tm2
        print(f"TIMING: {n_rows}:\t{tm_legacy/tm_v1}x\t{tm_legacy/tm_v2}x\t{tm_legacy/tm_legacy}x")

perf_check(n_repeat=5)

#####

def check_memory_leaks(n_rows=10_000, n_mem_checks=100_000_000, n_print=1_000_000):
    print("***** CHECK FOR MEMORY LEAKS *****")
    t, col_sources, index_set = make_test_inputs(n_rows)

    for i in range(1,n_mem_checks+1):
        if i%n_print == 0:
            print(f"Memory leak check: {i}")
        tensor_1 = gather1(index_set, col_sources)
        tensor_2 = gather2(index_set, col_sources)

# check_memory_leaks()



 */


/**
 * Example of copying data from a table into a tensor.
 *
 * 1. One of these two should be much faster than the other.
 *    I would guess that V2 is faster because of less fragmented memory accesses, and that seems to be what my tests show.
 * 2. There need to be many of these functions with different tensor types to handle different numpy inputs.
 * 3. It is possible that this could be even faster by using the chunked interface.  Discuss with Cristian.
 *    May or may not be worth the work.  Already seeing speedups of 10-200x.
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

    /**
     * Copy data from a table into a 2d tensor.
     *
     * @param indexSet indices of the rows of the table to put into the tensor
     * @param columnSources columns of data to put into the tensor
     * @return  contiguous RAM allocated for the tensor.  When a numpy tensor is passed in for this argument, jpy will handle passing the memory reference as a 1d java array here.
     */
    public static double[] create_tensor_2d_v1(final IndexSet indexSet, final ColumnSource<?>[] columnSources) {
//        final long tstart = System.currentTimeMillis();

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
//        final long tend = System.currentTimeMillis();
//        System.out.println("TIME: V1 (" + nRows + ") = " + (tend-tstart));
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
//        final long tstart = System.currentTimeMillis();

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
//        final long tend = System.currentTimeMillis();
//        System.out.println("TIME: V2 (" + nRows + ") = " + (tend-tstart));
        return tensor;
    }

}