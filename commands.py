from database import DatabaseManager
import sys
import datetime

# bookmark.db will be created when this module is imported or run directly
db = DatabaseManager('bookmarks.db')

class CreateBookmarksTableCommand:

    def execute(self):
        db.create_table('bookmarks', {'id':'integer primary key AUTOINCREMENT',
                                      'title': 'text not null',
                                      'url': 'text not null',
                                      'notes': 'text',
                                      'date_added': 'text not null'
                                      })


class AddBookmarkCommand:

    def execute(self, bookmark):
        bookmark['date_added'] = datetime.datetime.utcnow().isoformat()
        db.add('bookmarks', bookmark)
        return 'Bookmark added!'


class ListBookmarksCommand:

    def __init__(self, order_by=None):
        self.order_by = order_by

    def execute(self):
        return db.select('bookmarks', order_by=self.order_by).fetchall()


class DeleteBookmarkCommand:

    def execute(self, id):
        db.delete('bookmarks', {'id':id})
        return 'Bookmark deleted!'


class QuitCommand:

    def execute(self):
        sys.exit()
