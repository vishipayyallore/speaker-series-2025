using System.Collections;

namespace CS13Features.ParamsCollections;

internal sealed class CustomCollection : IEnumerable<int>
{
    private readonly List<int> _internalList = [];

    public void Add(int number)
    {
        _internalList.Add(number);
    }

    public IEnumerator<int> GetEnumerator()
    {
        return _internalList.GetEnumerator();
    }

    IEnumerator IEnumerable.GetEnumerator()
    {
        return GetEnumerator();
    }
}
