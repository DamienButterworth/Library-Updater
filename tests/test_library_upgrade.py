from pyfakefs.fake_filesystem_unittest import TestCase

from src.library_updater import library_upgrade


class LibraryUpgrade(TestCase):
    def setUp(self):
        self.setUpPyfakefs()

    def test_get_libraries(self):
        self.fs.create_file('test.scala', contents="    \"org.mockito\"             %% \"mockito-scala-scalatest\"    % \"1.5.12\"  % \"test,it\"")
        self.fs.create_file('test.sbt')
        self.fs.create_file('test.ignored')

        result = library_upgrade.get_libraries()
        assert result[0].group(2) == "mockito-scala-scalatest"

    def test_get_sbt_plugin_version(self):
        self.fs.create_file('test.sbt', contents="addSbtPlugin(\"com.typesafe.play\" % \"sbt-plugin\" % \"2.6.20\")")
        result = library_upgrade.get_sbt_plugin_version()
        assert result == "2.6.20"


