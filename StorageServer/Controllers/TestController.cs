using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace StorageServer.Controllers;

[Route("/test")]
[ApiController]
public class TestController : ControllerBase
{
    [Authorize]
    [HttpGet("private")]
    public IActionResult AuthorizedMethod()
    {
        return Ok("Success");
    }

    [HttpGet("public")]
    public IActionResult PublicMethod()
    {
        return Ok("Success");
    }
}
