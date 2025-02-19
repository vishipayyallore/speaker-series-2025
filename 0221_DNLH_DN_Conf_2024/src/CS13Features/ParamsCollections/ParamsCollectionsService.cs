namespace CS13Features.ParamsCollections;

internal static class ParamsCollectionsService
{
    public static void ShowDemo()
    {
        ForegroundColor = ConsoleColor.DarkCyan;

        WriteLine("=== Params Collections Demo ===");

        ShowNumbersArray(21, 18, 93);

        ShowNumbersEnumerable(36, 87, 62, 37, 91, 38, 66);

        ShowNumbersList(38, 9, 56, 94, 6, 33, 97);

        ShowNumbersCustomCollection(92, 57, 93, 15, 55, 92);

        ShowNumbersReadOnlySpan(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        ResetColor();
    }

    static void ShowNumbersArray(params int[] numbers)
    {
        WriteLine("Showing numbers array:");
        
        WriteLine(string.Join(" ", numbers));
    }

    static void ShowNumbersEnumerable(params IEnumerable<int> numbers)
    {
        WriteLine("Showing numbers enumerable:");

        WriteLine(string.Join(" ", numbers));
    }

    static void ShowNumbersList(params List<int> numbers)
    {
        WriteLine("Showing numbers list:");

        WriteLine(string.Join(" ", numbers));
    }

    static void ShowNumbersReadOnlySpan(params ReadOnlySpan<int> numbers)
    {
        WriteLine("Showing numbers read-only span:");
        for (int i = 0; i < numbers.Length; i++)
        {
            Write($"{numbers[i]} ");
        }
        WriteLine();
    }

    static void ShowNumbersCustomCollection(params CustomCollection numbers)
    {
        WriteLine("Showing numbers custom collection:");

        WriteLine(string.Join(" ", numbers));
    }

}
