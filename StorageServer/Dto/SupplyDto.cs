namespace StorageServer.Dto;

public class SupplyDto
{
    public int Id { get; set; }
    public int SupplierId { get; set; }
    public DateTimeOffset RealDate { get; set; }
    public DateTimeOffset PlannedDate { get; set; }
    public ICollection<SupplyUnitDto> SupplyUnits { get; set; } = [];
}
