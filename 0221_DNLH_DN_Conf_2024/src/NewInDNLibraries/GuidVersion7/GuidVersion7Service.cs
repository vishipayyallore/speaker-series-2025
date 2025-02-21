namespace NewInDNLibraries.GuidVersion7;

internal static class GuidVersion7Service
{
    public static void ShowDemo()
    {
        ForegroundColor = ConsoleColor.Green;

        WriteLine("***** Generating GUIDs with Version 7 Demo *****\n");

        WriteLine("- GENERATING REGULAR GUIDs -");
        for (int i = 0; i < 5; i++)
        {
            var guid = Guid.NewGuid();
            WriteLine($"Version: {GetGuidVersion(guid)}, GUID: {guid}");
        }

        WriteLine();

        ForegroundColor = ConsoleColor.Yellow;

        WriteLine("- GENERATING VERSION 7 GUIDs -");
        for (int i = 0; i < 5; i++)
        {
            var guid = Guid.CreateVersion7();
            WriteLine($"Version: {GetGuidVersion(guid)}, GUID: {guid}");
        }

        WriteLine();

        ResetColor();
    }

    // Helper method to extract the GUID version
    private static int GetGuidVersion(Guid guid)
    {
        var bytes = guid.ToByteArray();
        return (bytes[7] >> 4) & 0x0F;
    }
}