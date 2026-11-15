if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

@transformer
def validate(df, *args, **kwargs):
    print('Missing values:', int(df.isnull().sum().sum()), '| Classes:', df['target'].nunique())
    return df

@test
def test_output(output, *args):
    assert output.isnull().sum().sum() == 0, 'Missing values found'
    assert output['target'].nunique() == 3, 'Expected exactly 3 classes'
