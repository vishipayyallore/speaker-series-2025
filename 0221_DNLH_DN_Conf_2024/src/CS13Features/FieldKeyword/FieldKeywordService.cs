namespace CS13Features.FieldKeyword;

internal static class FieldKeywordService
{
    public static void ShowDemo()
    {
        ForegroundColor = ConsoleColor.Cyan;

        WriteLine("\n=== Field Keyword Demo in C# 13 ===\n");

        try
        {
            var product = new Product
            {
                Name = "  Widget  ",
                Price = 19.99m
            };

            WriteLine($"Product: {product.Name}");
            WriteLine($"Price: {product.Price:C}");
            WriteLine($"Description: {product.Description}");
        }
        catch (Exception ex)
        {
            WriteLine($"Error creating product: {ex.Message}");
        }

        WriteLine("\n=== Testing Invalid Inputs ===\n");

        var testProduct = new Product { Name = "Valid Product" };

        try
        {
            testProduct.Name = ""; // Should throw an exception
        }
        catch (ArgumentException ex)
        {
            WriteLine($"Error: {ex.Message}");
        }

        try
        {
            testProduct.Price = -5; // Should throw an exception
        }
        catch (ArgumentException ex)
        {
            WriteLine($"Error: {ex.Message}");
        }

        ResetColor();
    }
}