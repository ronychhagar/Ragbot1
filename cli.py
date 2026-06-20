#!/usr/bin/env python3
"""
RAG Bot Management CLI
Utility for managing the RAG system from command line
"""

import argparse
import sys
from pathlib import Path

from ingest import ingest_documents, ingest_single_document
from rag_engine import get_rag_engine
from storage.vector_store import get_vector_store
from utils.logger import log_info, log_error


def ingest_command(args):
    """Handle document ingestion"""
    if args.file:
        log_info(f"Ingesting single file: {args.file}")
        result = ingest_single_document(args.file)
    else:
        log_info("Ingesting all documents from data directory")
        result = ingest_documents()
    
    print("\n" + "="*60)
    print(f"Status: {result['status'].upper()}")
    print(f"Message: {result.get('message', 'N/A')}")
    
    if 'documents_loaded' in result:
        print(f"Documents loaded: {result['documents_loaded']}")
    if 'chunks_created' in result:
        print(f"Chunks created: {result['chunks_created']}")
    if 'chunks_ingested' in result:
        print(f"Chunks ingested: {result['chunks_ingested']}")
    if 'chunks' in result:
        print(f"Chunks: {result['chunks']}")
    
    print("="*60 + "\n")
    
    return 0 if result['status'] == 'success' else 1


def query_command(args):
    """Handle RAG queries"""
    engine = get_rag_engine(args.session)
    
    print(f"\n🤖 Querying with session: {args.session}")
    print(f"📝 Question: {args.question}\n")
    
    result = engine.ask(args.question, use_memory=not args.no_memory)
    
    print("="*60)
    print("ANSWER:")
    print("="*60)
    print(result['answer'])
    
    if result.get('sources'):
        print("\n" + "="*60)
        print(f"SOURCES ({len(result['sources'])}):")
        print("="*60)
        for i, source in enumerate(result['sources'], 1):
            print(f"\n[Source {i}]")
            print(f"Content: {source.get('content', '')[:200]}...")
            print(f"Confidence: {source.get('confidence', 0):.2%}")
    
    print("\n")
    return 0


def info_command(args):
    """Show vector store info"""
    store = get_vector_store()
    info = store.get_collection_info()
    
    print("\n" + "="*60)
    print("VECTOR STORE INFO")
    print("="*60)
    print(f"Collection Name: {info.get('name', 'Unknown')}")
    print(f"Document Count: {info.get('count', 0)}")
    print("="*60 + "\n")


def memory_command(args):
    """Show memory info for a session"""
    engine = get_rag_engine(args.session)
    summary = engine.get_memory_summary()
    
    print("\n" + "="*60)
    print(f"MEMORY INFO - Session: {args.session}")
    print("="*60)
    print(f"Total Messages: {summary['total_messages']}")
    print(f"User Messages: {summary['user_messages']}")
    print(f"Assistant Messages: {summary['assistant_messages']}")
    print(f"Context Length: {summary['context_length']} characters")
    print("="*60 + "\n")


def clear_command(args):
    """Clear session memory"""
    engine = get_rag_engine(args.session)
    engine.clear_memory()
    print(f"\n✅ Cleared memory for session: {args.session}\n")


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="RAG Bot Management CLI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python cli.py ingest                    # Ingest all documents
  python cli.py ingest --file data.pdf   # Ingest single file
  python cli.py query "What is BMW?"     # Ask a question
  python cli.py info                      # Show vector store info
  python cli.py memory --session user_1   # Show session memory
  python cli.py clear --session user_1    # Clear session memory
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Command to execute')
    
    # Ingest command
    ingest_parser = subparsers.add_parser('ingest', help='Ingest documents')
    ingest_parser.add_argument('--file', help='Single file to ingest')
    ingest_parser.set_defaults(func=ingest_command)
    
    # Query command
    query_parser = subparsers.add_parser('query', help='Ask a question')
    query_parser.add_argument('question', help='Question to ask')
    query_parser.add_argument('--session', default='default', help='Session ID')
    query_parser.add_argument('--no-memory', action='store_true', help='Disable conversation memory')
    query_parser.set_defaults(func=query_command)
    
    # Info command
    subparsers.add_parser('info', help='Show vector store info').set_defaults(func=info_command)
    
    # Memory command
    memory_parser = subparsers.add_parser('memory', help='Show session memory')
    memory_parser.add_argument('--session', default='default', help='Session ID')
    memory_parser.set_defaults(func=memory_command)
    
    # Clear command
    clear_parser = subparsers.add_parser('clear', help='Clear session memory')
    clear_parser.add_argument('--session', default='default', help='Session ID')
    clear_parser.set_defaults(func=clear_command)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        log_error(f"CLI Error: {str(e)}")
        print(f"\n❌ Error: {str(e)}\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
