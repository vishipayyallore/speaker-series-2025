namespace CS13Features.OverloadResolutionPriorityProperty;

internal static class OverloadResolutionPriorityPropertyServices
{
    public static void ShowDemo()
    {
        ForegroundColor = ConsoleColor.DarkYellow;

        WriteLine("\n=== Overload Resolution Priority Demo ===\n");

        Numbers.PerformAction(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        ResetColor();
    }
}
