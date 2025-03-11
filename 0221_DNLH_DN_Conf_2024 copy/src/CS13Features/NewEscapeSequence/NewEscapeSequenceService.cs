namespace CS13Features.NewEscapeSequence;

internal static class NewEscapeSequenceService
{
    private static readonly Dictionary<string, string> Colors = new()
    {
        { "Red", "31" },
        { "Green", "32" },
        { "Blue", "34" },
        { "Yellow", "33" },
        { "Cyan", "36" }
    };

    private static readonly Dictionary<string, string> Styles = new()
    {
        { "Bold", "1" },
        { "Underline", "4" },
        { "Reset", "0" }
    };

    public static void ShowDemo()
    {
        WriteLine("\n=== Demonstrating Old Escape Sequences (Pre .NET 9) ===\n");

        // Old Escape Sequences (Pre .NET 9)
        string redTextOld = "\u001b[31mThis text is red!\u001b[0m";
        string greenTextOld = "\u001b[32mThis text is green!\u001b[0m";

        WriteLine(redTextOld);
        WriteLine(greenTextOld);

        // New Escape Sequences (.NET 9)
        ForegroundColor = ConsoleColor.DarkCyan;
        WriteLine("\n\n=== Demonstrating New Escape Sequences (.NET 9) ===\n");

        foreach (var style in Styles)
        {
            foreach (var color in Colors)
            {
                string formattedText = GetFormattedText($"{style.Key} {color.Key}", color.Value, style.Value);
                WriteLine(formattedText);
            }
        }

        ResetColor();
    }

    private static string GetFormattedText(string text, string colorCode, string styleCode)
    {
        return $"\e[{styleCode};{colorCode}m{text}\e[0m";
    }
}
