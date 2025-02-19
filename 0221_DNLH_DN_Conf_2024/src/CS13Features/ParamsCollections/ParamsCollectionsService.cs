namespace CS13Features.ParamsCollections;

internal static class ParamsCollectionsService
{
    public static void ShowDemo()
    {
        ForegroundColor = ConsoleColor.DarkCyan;

        ShowNumbersArray(21, 18, 93);

        ShowNumbersEnumerable(36, 87, 62, 37, 91, 38, 66);

        ShowNumbersList(38, 9, 56, 94, 6, 33, 97);

        ShowNumbersCustomCollection(92, 57, 93, 15, 55, 92);

        ShowNumbersReadOnlySpan(1, 2, 3, 4, 5, 6, 7, 8, 9, 10);

        ResetColor();
    }

    static void ShowNumbersArray(params int[] numbers)
    {
        Console.WriteLine("Showing numbers array:");

        for (int i = 0; i < numbers.Length; i++)
        {
            Console.Write(numbers[i]);
            Console.Write(" ");
        }
        Console.WriteLine();
    }

    static void ShowNumbersEnumerable(params IEnumerable<int> numbers)
    {
        Console.WriteLine("Showing numbers enumerable:");
        for (int i = 0; i < numbers.Count(); i++)
        {
            Console.Write(numbers.ToList()[i]);
            Console.Write(" ");
        }
        Console.WriteLine();
    }

    static void ShowNumbersList(params List<int> numbers)
    {
        Console.WriteLine("Showing numbers list:");
        for (int i = 0; i < numbers.Count; i++)
        {
            Console.Write(numbers[i]);
            Console.Write(" ");
        }
        Console.WriteLine();
    }

    static void ShowNumbersReadOnlySpan(params ReadOnlySpan<int> numbers)
    {
        Console.WriteLine("Showing numbers read-only span:");
        for (int i = 0; i < numbers.Length; i++)
        {
            Console.Write(numbers[i]);
            Console.Write(" ");
        }
        Console.WriteLine();
    }

    static void ShowNumbersCustomCollection(params CustomCollection numbers)
    {
        Console.WriteLine("Showing numbers custom collection:");
        for (int i = 0; i < numbers.Count(); i++)
        {
            Console.Write(numbers.ToList()[i]);
            Console.Write(" ");
        }
        Console.WriteLine();
    }



}
