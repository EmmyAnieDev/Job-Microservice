<?php

use App\Models\User;
use Illuminate\Foundation\Testing\RefreshDatabase;

uses(RefreshDatabase::class);


/**
 * 🚀 Register Test
 */
it('registers a user successfully', function () {
    $response = $this->postJson('/api/v1/auth/register', [
        'name' => 'John Doe',
        'email' => 'john@example.com',
        'password' => 'password123',
        'password_confirmation' => 'password123',
    ]);

    $response->assertStatus(201)
        ->assertJson([
            'success' => true,
            'message' => 'User registered successfully.',
        ]);

    expect(User::where('email', 'john@example.com')->exists())->toBeTrue();
});


/**
 * 🔐 Login Success Test
 */
it('logs in a user with correct credentials', function () {
    User::factory()->create([
        'email' => 'john@example.com',
        'password' => bcrypt('password123'),
    ]);

    $response = $this->postJson('/api/v1/auth/login', [
        'email' => 'john@example.com',
        'password' => 'password123',
    ]);

    $response->assertStatus(200)
        ->assertJsonStructure([
            'success',
            'message',
            'data' => [
                'access_token',
                'refresh_token',
            ]
        ]);
});


/**
 * ❌ Login Failure Test
 */
it('rejects login with invalid credentials', function () {
    $response = $this->postJson('/api/v1/auth/login', [
        'email' => 'invalid@example.com',
        'password' => 'wrongpassword',
    ]);

    $response->assertStatus(401)
        ->assertJson([
            'success' => false,
            'message' => 'Invalid credentials.',
        ]);
});


/**
 * 🔄 Refresh Token Test
 */
it('refreshes the access token successfully', function () {
    // Create user
    $user = User::factory()->create([
        'email' => 'john@example.com',
        'password' => bcrypt('password123'),
    ]);

    // Login to get the refresh token
    $loginResponse = $this->postJson('/api/v1/auth/login', [
        'email' => 'john@example.com',
        'password' => 'password123',
    ]);

    $refreshToken = $loginResponse->json('data.refresh_token');

    // Call refresh endpoint with the refresh token
    $response = $this->withHeader('Authorization', "Bearer $refreshToken")
        ->postJson('/api/v1/auth/refresh');

    $response->assertStatus(200)
        ->assertJson([
            'success' => true,
            'message' => 'Token refreshed successfully.',
        ])
        ->assertJsonStructure([
            'success',
            'message',
            'data' => [
                'access_token',
                'refresh_token',
            ]
        ]);
});


/**
 * 🔓 Logout Test
 */
it('logs out an authenticated user', function () {
    $user = User::factory()->create([
        'email' => 'john@example.com',
        'password' => bcrypt('password123'),
    ]);

    $loginResponse = $this->postJson('/api/v1/auth/login', [
        'email' => 'john@example.com',
        'password' => 'password123',
    ]);

    $token = $loginResponse->json('data.access_token');

    $response = $this->withHeader('Authorization', "Bearer $token")
        ->postJson('/api/v1/auth/logout');

    $response->assertStatus(200)
        ->assertJson([
            'success' => true,
            'message' => 'Logged out successfully.',
        ]);
});
