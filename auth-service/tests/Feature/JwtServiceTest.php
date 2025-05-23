<?php

namespace Tests\Feature;

use App\Services\V1\JwtService;
use Illuminate\Support\Facades\Redis;
use Tests\TestCase;

class JwtServiceTest extends TestCase
{
    protected $jwtService;

    protected function setUp(): void
    {
        parent::setUp();

        // Mock env variables (override in runtime)
        config([
            'app.key' => 'base64:' . base64_encode(random_bytes(32)),
        ]);

        putenv('JWT_SECRET=test-secret');
        putenv('JWT_ALGORITHM=HS256');
        putenv('ACCESS_TIME_TO_LIVE=3600');
        putenv('REFRESH_TIME_TO_LIVE=7200');
        putenv('JTI_TIME_TO_LIVE=3600');

        $this->jwtService = new JwtService();

        Redis::flushall(); // Clear Redis for clean state
    }

    public function testItCreatesAndDecodesAccessToken()
    {
        $token = $this->jwtService->createAccessToken(1, 'test@example.com');

        $this->assertIsString($token);

        $decoded = $this->jwtService->decodeToken($token);

        $this->assertEquals(1, $decoded['sub']);
        $this->assertEquals('access', $decoded['type']);
    }

    public function testItCreatesAndDecodesRefreshToken()
    {
        $token = $this->jwtService->createRefreshToken(2, 'refresh@example.com');

        $decoded = $this->jwtService->decodeToken($token);

        $this->assertEquals(2, $decoded['sub']);
        $this->assertEquals('refresh', $decoded['type']);
    }

    public function testItValidatesValidAccessToken()
    {
        $token = $this->jwtService->createAccessToken(1, 'test@example.com');

        $validated = $this->jwtService->validateToken($token, 'access');

        $this->assertIsArray($validated);
        $this->assertEquals('access', $validated['type']);
    }

    public function testItInvalidatesTokenIfTypeDoesNotMatch()
    {
        $token = $this->jwtService->createRefreshToken(3, 'wrongtype@example.com');

        $validated = $this->jwtService->validateToken($token, 'access');

        $this->assertFalse($validated);
    }

    public function testItRevokesTokenAndDetectsRevocation()
    {
        $token = $this->jwtService->createAccessToken(4, 'revoke@example.com');
        $this->jwtService->revokeToken($token);

        usleep(100000); // wait for Redis

        $revoked = $this->jwtService->isRevoked($token);

        // Debug output:
        var_dump($revoked);
        $this->assertTrue($revoked, 'Token should be marked as revoked in Redis');

        $this->assertFalse($this->jwtService->validateToken($token, 'access'));
    }



    public function testItReturnsNullIfDecodingInvalidToken()
    {
        $decoded = $this->jwtService->decodeToken('invalid.token.here');

        $this->assertNull($decoded);
    }
}
