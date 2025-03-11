namespace CS13Features.FieldKeyword;

internal sealed class Product
{
    public required string Name
    {
        get => field;

        set
        {
            if (string.IsNullOrWhiteSpace(value))
            {
                throw new ArgumentException("Product name cannot be empty or null.");
            }

            field = value.Trim();
        }
    }

    public decimal Price
    {
        get => field;

        set
        {
            if (value < 0)
            {
                throw new ArgumentException("Price cannot be negative.");
            }
            field = value;
        }

    } = 9.99m; // Default price

    public string Description => $"{Name} - {Price:C}"; // Auto-formatted currency output
}