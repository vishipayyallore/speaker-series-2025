using System.Text;
using System.Buffers.Text;

namespace NewInDNLibraries.Base64UrlLib;

internal static class Base64UrlService
{
    public static void ShowDemo()
    {
        string[] samples =
        {
            "Hello, .NET 9!",
            "C# 13 is awesome 🚀",
            "Encode this: @+#$%^&*/()_",
            "URL Safe: https://example.com?query=net9&name=Sri+Varu"
        };

        ForegroundColor = ConsoleColor.Cyan;

        WriteLine("Base64 and Base64Url Encoding Demo\n");

        foreach (var text in samples)
        {
            byte[] toEncodeAsBytes = Encoding.UTF8.GetBytes(text);

            string base64 = Convert.ToBase64String(toEncodeAsBytes);

            string base64Url = Base64Url.EncodeToString(toEncodeAsBytes);

            WriteLine($"Original: {text}");
            WriteLine($"Base64: {base64}");
            WriteLine($"Base64Url: {base64Url}\n");
        }

        ResetColor();
    }

}
