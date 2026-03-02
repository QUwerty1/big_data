namespace StorageServer.DTO;

public record CustomerDTO(
    string CompanyName,
    string Phone,
    string Address,
    string Email,
    int? Id = null,
    string? AppUserId = null
);