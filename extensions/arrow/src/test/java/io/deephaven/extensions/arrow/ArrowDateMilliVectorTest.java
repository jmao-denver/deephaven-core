//
// Copyright (c) 2016-2025 Deephaven Data Labs and Patent Pending
//
// ****** AUTO-GENERATED CLASS - DO NOT EDIT MANUALLY
// ****** Run GenerateArrowColumnSourceTests or "./gradlew generateArrowColumnTestSources" to regenerate
//
// @formatter:off
package io.deephaven.extensions.arrow;

import io.deephaven.chunk.WritableObjectChunk;
import io.deephaven.chunk.attributes.Values;
import io.deephaven.engine.table.ChunkSource;
import io.deephaven.engine.table.ColumnSource;
import io.deephaven.engine.table.impl.QueryTable;
import io.deephaven.engine.testutil.junit4.EngineCleanup;
import io.deephaven.util.mutable.MutableInt;
import java.io.File;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Rule;
import org.junit.Test;

public class ArrowDateMilliVectorTest {
    private static final List<Long> expectedRows = Arrays.asList(0L, 1L, 2L, 4L, 8L, 9L);

    private static final LocalDateTime[] expectedValues = new LocalDateTime[] {java.time.LocalDateTime.of(2022, 11, 30, 23, 0, 0), java.time.LocalDateTime.of(2000, 1, 16, 23, 0, 0), null, java.time.LocalDateTime.of(2022, 1, 31, 22, 8, 2), java.time.LocalDateTime.of(1920, 1, 31, 23, 8, 2), java.time.LocalDateTime.of(1900, 1, 31, 23, 22, 46)};

    @Rule
    public final EngineCleanup framework = new EngineCleanup();

    private static QueryTable loadTable() {
        //noinspection ConstantConditions;
        final File dataFile = new File(ArrowDateMilliVectorTest.class.getResource("/date_milli_vector.arrow").getFile());
        return ArrowWrapperTools.readFeather(dataFile.getPath());
    }

    @Test
    public void testReadArrowFile() {
        final QueryTable table = loadTable();
        Assert.assertEquals(expectedValues.length, table.intSize());

        // check that the expected rows are present;
        final List<Long> actualRows = new ArrayList<>();
        table.getRowSet().forAllRowKeys(actualRows::add);
        Assert.assertEquals(expectedRows, actualRows);

        Assert.assertEquals(1, table.getColumnSources().size());
        // noinspection OptionalGetWithoutIsPresent, unchecked;
        final ColumnSource<LocalDateTime> cs = (ColumnSource<LocalDateTime>)table.getColumnSources().stream().findFirst().get();

        ArrowWrapperTools.Shareable.resetNumBlocksLoaded();
        final MutableInt pos = new MutableInt();
        table.getRowSet().forAllRowKeys(rowKey -> Assert.assertEquals(expectedValues[pos.getAndIncrement()], cs.get(rowKey)));
        Assert.assertEquals(3, ArrowWrapperTools.Shareable.numBlocksLoaded());
    }

    @Test
    public void testFillChunk() {
        final QueryTable table = loadTable();

        // noinspection OptionalGetWithoutIsPresent, unchecked;
        final ColumnSource<LocalDateTime> cs = (ColumnSource<LocalDateTime>)table.getColumnSources().stream().findFirst().get();

        try (final ChunkSource.FillContext fillContext = cs.makeFillContext(table.intSize());
            final WritableObjectChunk<LocalDateTime, Values> chunk = WritableObjectChunk.makeWritableChunk(table.intSize())) {

            ArrowWrapperTools.Shareable.resetNumBlocksLoaded();
            cs.fillChunk(fillContext, chunk, table.getRowSet());
            Assert.assertEquals(3, ArrowWrapperTools.Shareable.numBlocksLoaded());

            for (int ii = 0; ii < expectedValues.length; ++ii) {
                Assert.assertEquals(expectedValues[ii], chunk.get(ii));
            }
        }
    }
}
