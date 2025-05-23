<?php

use App\Traits\Api\v1\ApiResponse;
use Illuminate\Http\JsonResponse;

uses()->group('api-response');

beforeEach(function () {
    // Create a dummy class that uses the trait for testing
    $this->dummy = new class {
        use ApiResponse;

        public function success($data, $message = null, $status = 200)
        {
            return $this->successResponse($data, $message, $status);
        }

        public function error($message, $status = 400)
        {
            return $this->errorResponse($message, $status);
        }
    };
});

it('returns a success JSON response with proper structure and status', function () {
    $data = ['foo' => 'bar'];
    $message = 'Operation successful';
    $status = 201;

    $response = $this->dummy->success($data, $message, $status);

    expect($response)->toBeInstanceOf(JsonResponse::class);

    $json = $response->getData(true);

    expect($json['success'])->toBeTrue();
    expect($json['message'])->toBe($message);
    expect($json['data'])->toBe($data);
    expect($json['status'])->toBe($status);
    expect($response->getStatusCode())->toBe($status);
});

it('returns an error JSON response with proper structure and status', function () {
    $message = 'Something went wrong';
    $status = 422;

    $response = $this->dummy->error($message, $status);

    expect($response)->toBeInstanceOf(JsonResponse::class);

    $json = $response->getData(true);

    expect($json['success'])->toBeFalse();
    expect($json['message'])->toBe($message);
    expect($json['status'])->toBe($status);
    expect($response->getStatusCode())->toBe($status);
});
