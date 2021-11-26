/* ---------------------------------------------------------------------------------------------------------------------
 * AUTO-GENERATED CLASS - DO NOT EDIT MANUALLY - for any changes edit TestCharSegmentedSortedArray and regenerate
 * ------------------------------------------------------------------------------------------------------------------ */
package io.deephaven.db.v2.ssa;

import io.deephaven.base.verify.AssertionFailure;
import io.deephaven.db.tables.Table;
import io.deephaven.db.tables.live.LiveTableMonitor;
import io.deephaven.db.util.liveness.LivenessScope;
import io.deephaven.db.util.liveness.LivenessScopeStack;
import io.deephaven.db.v2.*;
import io.deephaven.db.v2.sources.ColumnSource;
import io.deephaven.db.v2.sources.chunk.Attributes;
import io.deephaven.db.v2.sources.chunk.Attributes.KeyIndices;
import io.deephaven.db.v2.sources.chunk.Attributes.Values;
import io.deephaven.db.v2.sources.chunk.ShortChunk;
import io.deephaven.db.v2.sources.chunk.LongChunk;
import io.deephaven.db.v2.utils.Index;
import io.deephaven.db.v2.utils.IndexShiftData;
import io.deephaven.test.types.ParallelTest;
import io.deephaven.util.SafeCloseable;
import junit.framework.TestCase;
import org.jetbrains.annotations.NotNull;
import org.junit.experimental.categories.Category;

import java.util.Random;

import static io.deephaven.db.v2.TstUtils.*;

@Category(ParallelTest.class)
public class TestShortSegmentedSortedArray extends LiveTableTestCase {

    public void testInsertion() {
        final SsaTestHelpers.TestDescriptor desc = new SsaTestHelpers.TestDescriptor();
        for (int seed = 0; seed < 10; ++seed) {
            for (int tableSize = 100; tableSize <= 1000; tableSize *= 10) {
                for (int nodeSize = 8; nodeSize <= 2048; nodeSize *= 2) {
                    testUpdates(desc.reset(seed, tableSize, nodeSize), true, false);
                }
            }
        }
    }

    public void testRemove() {
        final SsaTestHelpers.TestDescriptor desc = new SsaTestHelpers.TestDescriptor();
        for (int seed = 0; seed < 20; ++seed) {
            for (int tableSize = 100; tableSize <= 10000; tableSize *= 10) {
                for (int nodeSize = 16; nodeSize <= 2048; nodeSize *= 2) {
                    testUpdates(desc.reset(seed, tableSize, nodeSize), false, true);
                }
            }
        }
    }

    public void testInsertAndRemove() {
        final SsaTestHelpers.TestDescriptor desc = new SsaTestHelpers.TestDescriptor();
        for (int seed = 0; seed < 10; ++seed) {
            for (int tableSize = 100; tableSize <= 10000; tableSize *= 10) {
                for (int nodeSize = 16; nodeSize <= 2048; nodeSize *= 2) {
                    testUpdates(desc.reset(seed, tableSize, nodeSize), true, true);
                }
            }
        }
    }

    public void testShifts() {
        final SsaTestHelpers.TestDescriptor desc = new SsaTestHelpers.TestDescriptor();
        for (int seed = 0; seed < 20; ++seed) {
            for (int tableSize = 10; tableSize <= 10000; tableSize *= 10) {
                for (int nodeSize = 16; nodeSize <= 2048; nodeSize *= 2) {
                    testShifts(desc.reset(seed, tableSize, nodeSize));
                }
            }
        }
    }

    private void testShifts(@NotNull final SsaTestHelpers.TestDescriptor desc) {
        final Random random = new Random(desc.seed());
        final TstUtils.ColumnInfo[] columnInfo;
        final QueryTable table = getTable(desc.tableSize(), random, columnInfo = initColumnInfos(new String[]{"Value"},
                SsaTestHelpers.getGeneratorForShort()));

        final Table asShort = SsaTestHelpers.prepareTestTableForShort(table);

        final ShortSegmentedSortedArray ssa = new ShortSegmentedSortedArray(desc.nodeSize());

        final ColumnSource<Short> valueSource = asShort.getColumnSource("Value");

        checkSsaInitial(asShort, ssa, valueSource, desc);

        try (final SafeCloseable ignored = LivenessScopeStack.open(new LivenessScope(true), true)) {
            final ShiftAwareListener asShortListener = new InstrumentedShiftAwareListenerAdapter((DynamicTable) asShort, false) {
                @Override
                public void onUpdate(Update upstream) {
                    try (final ColumnSource.GetContext checkContext = valueSource.makeGetContext(asShort.getIndex().getPrevIndex().intSize());
                         final Index relevantIndices = asShort.getIndex().getPrevIndex().clone()) {

                        checkSsa(ssa, valueSource.getPrevChunk(checkContext, relevantIndices).asShortChunk(), relevantIndices.asKeyIndicesChunk(), desc);
                    }

                    final int size = Math.max(upstream.modified.intSize() + Math.max(upstream.added.intSize(), upstream.removed.intSize()), (int) upstream.shifted.getEffectiveSize());
                    try (final ColumnSource.GetContext getContext = valueSource.makeGetContext(size);
                         final Index takeout = upstream.removed.union(upstream.getModifiedPreShift()).clone();) {
                        ssa.validate();

                        if (takeout.nonempty()) {
                            final ShortChunk<? extends Values> valuesToRemove = valueSource.getPrevChunk(getContext, takeout).asShortChunk();
                            ssa.remove(valuesToRemove, takeout.asKeyIndicesChunk());
                        }

                        ssa.validate();

                        try (final ColumnSource.GetContext checkContext = valueSource.makeGetContext(asShort.getIndex().getPrevIndex().intSize());
                             final Index relevantIndices = asShort.getIndex().getPrevIndex().minus(takeout).clone()) {
                            checkSsa(ssa, valueSource.getPrevChunk(checkContext, relevantIndices).asShortChunk(), relevantIndices.asKeyIndicesChunk(), desc);
                        }

                        if (upstream.shifted.nonempty()) {
                            final IndexShiftData.Iterator sit = upstream.shifted.applyIterator();
                            while (sit.hasNext()) {
                                sit.next();
                                try (Index indexToShift = table.getIndex().getPrevIndex().subindexByKey(sit.beginRange(), sit.endRange()).minus(upstream.getModifiedPreShift()).minus(upstream.removed).clone()) {
                                    if (indexToShift.empty()) {
                                        continue;
                                    }

                                    final ShortChunk<? extends Values> shiftValues = valueSource.getPrevChunk(getContext, indexToShift).asShortChunk();

                                    if (sit.polarityReversed()) {
                                        ssa.applyShiftReverse(shiftValues, indexToShift.asKeyIndicesChunk(), sit.shiftDelta());
                                    } else {
                                        ssa.applyShift(shiftValues, indexToShift.asKeyIndicesChunk(), sit.shiftDelta());
                                    }
                                }
                            }
                        }

                        ssa.validate();

                        try (Index putin = upstream.added.union(upstream.modified).clone()) {

                            try (final ColumnSource.GetContext checkContext = valueSource.makeGetContext(asShort.intSize());
                                 final Index relevantIndices = asShort.getIndex().minus(putin).clone();) {
                                checkSsa(ssa, valueSource.getChunk(checkContext, relevantIndices).asShortChunk(), relevantIndices.asKeyIndicesChunk(), desc);
                            }

                            if (putin.nonempty()) {
                                final ShortChunk<? extends Values> valuesToInsert = valueSource.getChunk(getContext, putin).asShortChunk();
                                ssa.insert(valuesToInsert, putin.asKeyIndicesChunk());
                            }
                        }

                        ssa.validate();
                    }
                }
            };
            ((DynamicTable) asShort).listenForUpdates(asShortListener);

            while (desc.advance(50)) {
                LiveTableMonitor.DEFAULT.runWithinUnitTestCycle(() ->
                        GenerateTableUpdates.generateShiftAwareTableUpdates(GenerateTableUpdates.DEFAULT_PROFILE, desc.tableSize(), random, table, columnInfo));

                try (final ColumnSource.GetContext getContext = valueSource.makeGetContext(asShort.intSize());
                     final Index index = asShort.getIndex().clone()) {

                    checkSsa(ssa, valueSource.getChunk(getContext, index).asShortChunk(), index.asKeyIndicesChunk(), desc);
                }
            }
        }
    }

    private void testUpdates(@NotNull final SsaTestHelpers.TestDescriptor desc, boolean allowAddition, boolean allowRemoval) {
        final Random random = new Random(desc.seed());
        final TstUtils.ColumnInfo[] columnInfo;
        final QueryTable table = getTable(desc.tableSize(), random, columnInfo = initColumnInfos(new String[]{"Value"},
                SsaTestHelpers.getGeneratorForShort()));

        final Table asShort = SsaTestHelpers.prepareTestTableForShort(table);

        final ShortSegmentedSortedArray ssa = new ShortSegmentedSortedArray(desc.nodeSize());

        final ColumnSource<Short> valueSource = asShort.getColumnSource("Value");

        checkSsaInitial(asShort, ssa, valueSource, desc);

        try (final SafeCloseable ignored = LivenessScopeStack.open(new LivenessScope(true), true)) {
            final Listener asShortListener = new InstrumentedListenerAdapter((DynamicTable) asShort, false) {
                @Override
                public void onUpdate(Index added, Index removed, Index modified) {
                    try (final ColumnSource.GetContext getContext = valueSource.makeGetContext(Math.max(added.intSize(), removed.intSize()))) {
                        if (removed.nonempty()) {
                            final ShortChunk<? extends Values> valuesToRemove = valueSource.getPrevChunk(getContext, removed).asShortChunk();
                            ssa.remove(valuesToRemove, removed.asKeyIndicesChunk());
                        }
                        if (added.nonempty()) {
                            ssa.insert(valueSource.getChunk(getContext, added).asShortChunk(), added.asKeyIndicesChunk());
                        }
                    }
                }
            };
            ((DynamicTable) asShort).listenForUpdates(asShortListener);

            while (desc.advance(50)) {
                LiveTableMonitor.DEFAULT.runWithinUnitTestCycle(() -> {
                    final Index[] notify = GenerateTableUpdates.computeTableUpdates(desc.tableSize(), random, table, columnInfo, allowAddition, allowRemoval, false);
                    assertTrue(notify[2].empty());
                    table.notifyListeners(notify[0], notify[1], notify[2]);
                });

                try (final ColumnSource.GetContext getContext = valueSource.makeGetContext(asShort.intSize());
                     final Index index = asShort.getIndex().clone()) {

                    checkSsa(ssa, valueSource.getChunk(getContext, index).asShortChunk(), index.asKeyIndicesChunk(), desc);
                }

                if (!allowAddition && table.size() == 0) {
                    break;
                }
            }
        }
    }

    private void checkSsaInitial(Table asShort, ShortSegmentedSortedArray ssa, ColumnSource<?> valueSource, @NotNull final SsaTestHelpers.TestDescriptor desc) {
        try (final ColumnSource.GetContext getContext = valueSource.makeGetContext(asShort.intSize());
             final Index index = asShort.getIndex().clone()) {
            final ShortChunk<? extends Values> valueChunk = valueSource.getChunk(getContext, index).asShortChunk();
            final LongChunk<Attributes.OrderedKeyIndices> tableIndexChunk = index.asKeyIndicesChunk();

            ssa.insert(valueChunk, tableIndexChunk);

            checkSsa(ssa, valueChunk, tableIndexChunk, desc);
        }
    }

    private void checkSsa(ShortSegmentedSortedArray ssa, ShortChunk<? extends Values> valueChunk, LongChunk<? extends KeyIndices> tableIndexChunk, @NotNull final SsaTestHelpers.TestDescriptor desc) {
        try {
            ssa.validate();
            ShortSsaChecker.checkSsa(ssa, valueChunk, tableIndexChunk);
        } catch (AssertionFailure | SsaChecker.SsaCheckException e) {
            TestCase.fail("Check failed at " + desc + ": " + e.getMessage());
        }
    }
}
