using System.IdentityModel.Tokens.Jwt;
using System.Security.Authentication;
using System.Security.Claims;
using System.Text;

using Microsoft.AspNetCore.Identity;
using Microsoft.IdentityModel.Tokens;

using StorageServer.Models;

namespace StorageServer.Services;

public class TokenService(
    IConfiguration configuration,
    UserManager<AppUser> userManager
)
{
    private readonly JwtSecurityTokenHandler _tokenHandler = new();

    public async Task<string> GenerateTokenAsync(string username)
    {
        var user = await userManager.FindByNameAsync(username);

        if (user == null)
            throw new AuthenticationException($"Пользователь с именем {username} не найден");

        var userClaims = new ClaimsIdentity([
            new Claim(ClaimTypes.Name, username),
        ]);
        
        if (user.IsStaff)
            userClaims.AddClaim(new Claim(ClaimTypes.Role, "Staff"));

        var tokenDescriptor = new SecurityTokenDescriptor
        {
            Subject = userClaims,
            Issuer = configuration["Jwt:Issuer"],
            Audience = configuration["Jwt:Audience"],
            Expires = DateTime.UtcNow + TimeSpan.FromHours(24),
            SigningCredentials = new SigningCredentials(
                new SymmetricSecurityKey(Encoding.ASCII.GetBytes(configuration["Jwt:Key"]!)),
                SecurityAlgorithms.HmacSha256Signature)
        };

        var token = _tokenHandler.CreateToken(tokenDescriptor);

        return _tokenHandler.WriteToken(token);
    }
}