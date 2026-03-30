namespace StorageServer.Dto;

public class SaleUnitDto
{
    public int Id { get; set; }
    public required int Amount { get; set; }
    public required int ProductId { get; set; }
    public required decimal Price { get; set; }
}
