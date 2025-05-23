<?php

namespace App\Traits\Api\v1;

trait ApiResponse
{
    protected function successResponse($data, $message = null, $status = 200)
    {
        return response()->json([
            'success' => true,
            'message' => $message,
            'data' => $data,
            'status' => $status
        ], $status);
    }

    protected function errorResponse($message, $status = 400)
    {
        return response()->json([
            'success' => false,
            'message' => $message,
            'status' => $status
        ], $status);
    }
}
