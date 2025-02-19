namespace CS13Features.NewEscapeSequence;

internal static class NewEscapeSequenceService
{
    private static readonly Dictionary<string, string> colors = new()
    {
            { "Red", "31" },
            { "Green", "32" },
            { "Blue", "34" },
            { "Yellow", "33" },
            { "Cyan", "36" }
        };

    private static readonly Dictionary<string, string> styles = new()
    {
            { "Bold", "1" },
            { "Underline", "4" },
            { "Reset", "0" }
        };

    public static void ShowDemo()
    {
        //Pre .NET 9
        WriteLine("Demonstrating all color & style using Old Escape Sequence:\n");
        string redText = "\u001b[31mThis text is red!\u001b[0m";
        string greenText = "\u001b[32mThis text is green!\u001b[0m";

        WriteLine(redText);
        WriteLine(greenText);

        // .NET 9
        ForegroundColor = ConsoleColor.DarkCyan;

        WriteLine("\n\nDemonstrating all color & style combinations using New Escape Sequence:\n");

        foreach (var style in styles)
        {
            foreach (var color in colors)
            {
                string formattedText = GetFormattedText($"{style.Key} {color.Key}", color.Value, style.Value);
                WriteLine(formattedText);
            }
        }

        ResetColor();
    }

    static string GetFormattedText(string text, string colorCode, string styleCode)
    {
        return $"\e[{styleCode};{colorCode}m{text}\e[0m";
    }
}
