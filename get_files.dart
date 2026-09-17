import 'dart:io';
import 'package:http/http.dart' as http;

/// Downloads an image from a URL and attempts to display it using the system's default viewer.
/// 
/// Args:
///   url: The URL of the image to download.
Future<void> downloadAndView(String url) async {
  try {
    print('Downloading image from: $url');
    
    // Headers to mimic a browser
    final headers = {
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    };

    final response = await http.get(Uri.parse(url), headers: headers);

    print('HTTP Status Code: ${response.statusCode}');
    final contentType = response.headers['content-type'] ?? '';
    print('Content Type: $contentType');

    if (response.statusCode >= 400) {
      print('HTTP Error: Status ${response.statusCode}');
      if (response.statusCode == 401 || response.statusCode == 403) {
        print('Access Denied: This URL requires authentication (login).');
      }
      return;
    }

    if (contentType.contains('text/html')) {
      print('\nWARNING: The URL returned an HTML page instead of an image.');
      print('This usually happens with cPanel URLs because they require a login session.');
      print('Try using the public website URL instead of the cPanel viewer link.');
      return;
    }

    // Save image to a temporary file
    final tempDir = Directory.systemTemp;
    final fileExtension = _getFileExtension(contentType, url);
    final tempFile = File('${tempDir.path}/temp_image$fileExtension');
    
    await tempFile.writeAsBytes(response.bodyBytes);
    print('Image saved to: ${tempFile.path}');

    // Display the image using the system's default viewer
    await _showImage(tempFile.path);
    print('Image display command triggered.');

  } catch (e) {
    print('An error occurred: $e');
  }
}

String _getFileExtension(String contentType, String url) {
  if (contentType.contains('image/jpeg')) return '.jpg';
  if (contentType.contains('image/png')) return '.png';
  if (contentType.contains('image/gif')) return '.gif';
  
  // Fallback to URL extension
  final uri = Uri.parse(url);
  final path = uri.path;
  if (path.contains('.')) {
    return path.substring(path.lastIndexOf('.'));
  }
  return '.jpg'; // default
}

Future<void> _showImage(String filePath) async {
  if (Platform.isWindows) {
    await Process.run('start', ['', filePath], runInShell: true);
  } else if (Platform.isMacOS) {
    await Process.run('open', [filePath]);
  } else if (Platform.isLinux) {
    await Process.run('xdg-open', [filePath]);
  }
}

void main() async {
  // Public URL example
  const publicUrl = 'http://www.mohamed.hexhost.online/assets/assets/book/part2/K2-004.jpg';
  
  await downloadAndView(publicUrl);
}
