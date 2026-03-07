namespace StorageServer.Dto;

public class SaleDto
{
    public required int Id { get; set; }
    public required int CustomerId { get; set; }
    public required DateTimeOffset RealDate { get; set; }
    public required DateTimeOffset PlannedDate { get; set; }
    public ICollection<SaleUnitDto> SaleUnits { get; set; } = [];
}
