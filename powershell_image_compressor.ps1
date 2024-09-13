# Prompt for the source directory
$sourceDir = Read-Host -Prompt "Enter the path to the source directory"

# Prompt for the destination directory
$destinationDir = Read-Host -Prompt "Enter the path to the destination directory"

# Create the destination directory if it doesn't exist
if (-not (Test-Path -Path $destinationDir)) {
    New-Item -Path $destinationDir -ItemType Directory
}

# Load the .NET assembly for image processing
Add-Type -AssemblyName System.Drawing

# Get all JPEG files in the source directory
$files = Get-ChildItem -Path $sourceDir -Filter *.jpg

foreach ($file in $files) {
    $sourcePath = $file.FullName
    $destinationPath = Join-Path -Path $destinationDir -ChildPath $file.Name
    
    # Load the image
    $image = [System.Drawing.Image]::FromFile($sourcePath)
    
    # Set the quality (0-100, where 100 is the best quality)
    $encoderParameters = New-Object System.Drawing.Imaging.EncoderParameters(1)
    $encoderParameter = New-Object System.Drawing.Imaging.EncoderParameter([System.Drawing.Imaging.Encoder]::Quality, 50L) # Adjust quality as needed
    $encoderParameters.Param[0] = $encoderParameter
    
    # Get the JPEG encoder
    $codecInfo = [System.Drawing.Imaging.ImageCodecInfo]::GetImageDecoders() | Where-Object { $_.FormatID -eq [System.Drawing.Imaging.ImageFormat]::Jpeg.Guid }
    
    # Save the image with compression
    $image.Save($destinationPath, $codecInfo, $encoderParameters)
    
    # Dispose of the image object
    $image.Dispose()
}

Write-Output "Image compression complete."
