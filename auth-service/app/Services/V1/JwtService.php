<?php

namespace App\Services\V1;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Illuminate\Support\Facades\Redis;

class JwtService
{
    protected $secret;
    protected $accessTtl;
    protected $refreshTtl;

    public function __construct()
    {
        $this->secret = env('JWT_SECRET');
        $this->accessTtl = env('ACCESS_TIME_TO_LIVE');
        $this->refreshTtl = env('REFRESH_TIME_TO_LIVE');
    }

    public function createAccessToken($userId, $email)
    {
        $payload = [
            'iss' => 'auth-service',
            'sub' => $userId,
            'email' => $email,
            'iat' => time(),
            'exp' => time() + $this->accessTtl,
            'type' => 'access'
        ];

        return JWT::encode($payload, $this->secret, env('JWT_ALGORITHM'));
    }

    public function createRefreshToken($userId, $email)
    {
        $payload = [
            'iss' => 'auth-service',
            'sub' => $userId,
            'email' => $email,
            'iat' => time(),
            'exp' => time() + $this->refreshTtl,
            'type' => 'refresh'
        ];

        return JWT::encode($payload, $this->secret, env('JWT_ALGORITHM'));
    }

    public function decodeToken($jwt)
    {
        try {
            return (array) JWT::decode($jwt, new Key($this->secret, env('JWT_ALGORITHM')));
        } catch (\Exception $e) {
            return null;
        }
    }

    public function isRevoked($token): bool
    {
        return Redis::exists($this->getRedisKey($token));
    }

    public function revokeToken($token)
    {
        Redis::setex($this->getRedisKey($token), env('JTI_TIME_TO_LIVE'), 'revoked');
    }

    protected function getRedisKey($token)
    {
        return 'revoked_token:' . sha1($token);
    }

    public function validateToken($token, $type = 'access')
    {
        $decoded = $this->decodeToken($token);

        if (!$decoded || $decoded['type'] !== $type || $this->isRevoked($token)) {
            return false;
        }

        return $decoded;
    }
}
