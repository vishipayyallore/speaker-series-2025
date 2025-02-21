namespace NewInDNLibraries.TaskWhenEachLib;

internal static class TaskWhenEachService
{
    public static async Task ShowDemo()
    {
        ForegroundColor = ConsoleColor.Cyan;

        WriteLine("***** Task.WhenAll and Task.WhenEach Demos *****\n");

        var computationTasks = Enumerable.Range(1, 5).Select(async id =>
        {
            var delay = Random.Shared.Next(500, 3000);
            await Task.Delay(delay); // Simulate work
            return new ComputationResult(id, delay, id * 2);
        });

        // Using Task.WhenAll
        WriteLine("Processing all computations with Task.WhenAll:");

        var allResults = await Task.WhenAll(computationTasks);

        foreach (var result in allResults)
        {
            WriteLine($"Computation {result.Id} finished in {result.Delay} ms. Result: {result.Value}");
        }

        ForegroundColor = ConsoleColor.DarkCyan;

        WriteLine("\nProcessing computations as they complete with Task.WhenEach:");

        // Using Task.WhenEach
        var computationTaskList = computationTasks.ToList();
        await foreach (var task in Task.WhenEach(computationTaskList))
        {
            var result = await task;
            WriteLine($"Computation {result.Id} finished in {result.Delay} ms. Result: {result.Value}");
        }

        ResetColor();
    }
}
