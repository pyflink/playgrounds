import org.apache.flink.configuration.CoreOptions;
import org.apache.flink.python.PythonOptions;
import org.apache.flink.table.api.EnvironmentSettings;
import org.apache.flink.table.api.TableEnvironment;
import org.apache.flink.types.Row;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;
import java.util.List;

public class BlinkBatchPythonUdfSqlJob {
	public static void main(String[] args) {
		TableEnvironment tEnv = TableEnvironment.create(
			EnvironmentSettings.newInstance().useBlinkPlanner().inBatchMode().build());
		tEnv.getConfig().getConfiguration().set(CoreOptions.DEFAULT_PARALLELISM, 1);
		tEnv.getConfig().getConfiguration().set(PythonOptions.USE_MANAGED_MEMORY, true);
		tEnv.executeSql("create temporary system function add_one as 'udfs.add_one' language python");

		tEnv.createTemporaryView("source", tEnv.fromValues(1L, 2L, 3L).as("a"));

		Iterator<Row> result = tEnv.executeSql("select add_one(a) as a from source").collect();

		List<Long> actual = new ArrayList<>();
		while (result.hasNext()) {
			Row r = result.next();
			actual.add((Long) r.getField(0));
		}

		List<Long> expected = Arrays.asList(2L, 3L, 4L);
		if (!actual.equals(expected)) {
			throw new AssertionError(String.format("The output result: %s is not as expected: %s!", actual, expected));
		}
	}
}