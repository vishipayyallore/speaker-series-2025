using System.Collections;

namespace CS13Features.ParamsCollections;

internal sealed class CustomCollection : IEnumerable<int>
{
    private readonly List<int> _internalList = [];

    public CustomCollection() { }

    public CustomCollection(IEnumerable<int> numbers)
    {
        _internalList.AddRange(numbers);
    }

    public void Add(int number)
    {
        _internalList.Add(number);
    }

    public IEnumerator<int> GetEnumerator() => _internalList.GetEnumerator();

    IEnumerator IEnumerable.GetEnumerator() => GetEnumerator();

    public override string ToString() => $"[{string.Join(", ", _internalList)}]";
}
