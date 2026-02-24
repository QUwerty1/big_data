using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;

namespace StorageServer.Controllers;

[Route("api/test")]
[ApiController]
public class TestController : ControllerBase
{
    [Authorize]
    [HttpGet]
    [Route("/private")]
    public IActionResult AuthorizedMethod()
    {
        return Ok("Success");
    }

    [HttpGet]
    [Route("/public")]

    public IActionResult PublicMethod()
    {
        return Ok("Success");
    }
}
