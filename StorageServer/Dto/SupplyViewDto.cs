namespace StorageServer.Dto;

public class SupplyViewDto
{
    public int Id { get; set; }
    public int SupplierId { get; set; }
    public DateTimeOffset RealDate { get; set; }
    public DateTimeOffset PlannedDate { get; set; }
    public ICollection<int> SupplyUnitIds { get; set; } = [];
}
