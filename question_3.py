# Answer - Yes they run in same database transaction as the caller

class TestModel(models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'assessment_app'

transaction_ids = []

@receiver(post_save, sender=TestModel)
def test_signal_handler(sender, instance, created, **kwargs):
    from django.db import connection
    connection_id = id(connection)
    in_atomic = transaction.get_connection().in_atomic_block
    
    print(f"Atomic block: {in_atomic}")
    print(f"Connection ID: {connection_id}")
    transaction_ids.append(('signal', connection_id, in_atomic))

def run_test_q3():
    from django.db import connection
    conn_id_before = id(connection)
    print(f"Connection ID: {conn_id_before}")
    print(f"In atomic: {transaction.get_connection().in_atomic_block}")
    
    TestModel.objects.create(name="Test1")
    print()
    
    print("-" * 50)
    with transaction.atomic():
        print(f"Before create - In transaction: {transaction.get_connection().in_atomic_block}")
        TestModel.objects.create(name="Test2")
        print(f"After signal - In transaction: {transaction.get_connection().in_atomic_block}")
    
    print("\n" + "=" * 50)
    print("The signal handler runs within the SAME TRANSACTION")
    print("context as the caller. If the caller is in a transaction, so is")
    print("the signal handler. This means signal and caller share the same")
    print("database transaction lifecycle.\n")
