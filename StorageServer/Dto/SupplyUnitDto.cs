namespace StorageServer.Dto;

public class SupplyUnitDto
{
    public required int Id { get; set; }
    public required int Amount { get; set; }
    public required int ProductId { get; set; }
    public required decimal Price { get; set; }
}
