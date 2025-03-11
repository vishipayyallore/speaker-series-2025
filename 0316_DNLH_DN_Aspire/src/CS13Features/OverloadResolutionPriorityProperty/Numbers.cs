using System.Runtime.CompilerServices;

namespace CS13Features.OverloadResolutionPriorityProperty;

public sealed class Numbers
{
    [OverloadResolutionPriority(1)]
    public static void PerformAction(params int[] numbers)
    {
        WriteLine("Performing action with array:");
        foreach (var num in numbers)
        {
            Write($"{num} ");
        }
        WriteLine();
    }

    public static void PerformAction(params Span<int> numbers)
    {
        WriteLine("Performing action with span:");
        foreach (var num in numbers)
        {
            Write($"{num} ");
        }
        WriteLine();
    }
}