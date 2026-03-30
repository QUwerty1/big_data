namespace StorageServer.Dto;

public class SaleViewDto
{
    public required int Id { get; set; }
    public required int CustomerId { get; set; }
    public required DateTimeOffset RealDate { get; set; }
    public required DateTimeOffset PlannedDate { get; set; }
    public ICollection<int> SaleUnitIds { get; set; } = [];
}
