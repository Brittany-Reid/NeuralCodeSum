@Test
public void testCopyFile() throws IOException {
    final Path tempDir = Files.createTempDirectory(getClass().getCanonicalName());
    try {
        final Path sourceFile = Paths
            .get("src/test/resources/org/apache/commons/io/dirs-1-file-size-1/file-size-1.bin");
        final Path targetFile = PathUtils.copyFileToDirectory(sourceFile, tempDir);
        assertTrue(Files.exists(targetFile));
        assertEquals(Files.size(sourceFile), Files.size(targetFile));
    } finally {
        PathUtils.deleteDirectory(tempDir);
    }
}