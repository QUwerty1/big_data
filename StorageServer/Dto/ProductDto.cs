namespace StorageServer.Dto;

public class ProductDto
{
    public required int Id { get; set; }
    public required string ProductName { get; set; }
    public required decimal Price { get; set; }
}
